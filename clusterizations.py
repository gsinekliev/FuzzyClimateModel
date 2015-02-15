from numpy import dot, array, sum as numpy_sum, zeros, outer, reshape


class FuzzyCMeans(object):
    def __init__(self, training_set, initial_conditions, fuzzyness_coefficient=2.):
        """ training_set
                Containing vector data of entries to be clusterized.
            initial_conditions
                Randomly generated initial membership degrees to all clusters
                for each item item in the training_set.
            fuzzyness_coefficient
                Used for reducing the number of iterations of FuzzyCMeans, this
                happens, because of powering membership_degrees matrix with it.
        """
        self.fuzzyness_coefficient = fuzzyness_coefficient
        self.__training_set        = array(training_set)
        self.__membership_degrees  = array(initial_conditions)
        self.__centers             = self.compute_centers()
        self.__iterations          = 0

    def __get_membership_degrees(self):
        return self.__membership_degrees
    membership_degrees = property(__get_membership_degrees, None)
    """ Returns matrix of membership degrees for each item in training_set.
    """

    def __get_training_set(self):
        return self.__training_set
    training_set = property(__get_training_set, None)
    """ Contains the initial vectors, on which is trained FuzzyCMeans.
    """

    def __get_centers(self):
        return self.__centers
    def __set_centers(self, centers):
        self.__centers = array(reshape(centers, self.__centers.shape))
    centers = property(__get_centers, __set_centers)
    """ Numpy array containingthe centers of the centroids.
    """

    def __get_iterations(self):
        return self.__iterations
    iterations = property(__get_iterations, None)
    """ Integer containing how many iterations were needed for clusterization.
    """

    def compute_centers(self):
        mm = self.__membership_degrees ** self.fuzzyness_coefficient
        c = dot(self.__training_set.transpose(), mm) / numpy_sum(mm, axis=0)
        self.__centers = c.transpose()
        return self.__centers

    def membership(self):
        x = self.__training_set
        c = self.__centers
        M, _ = x.shape
        C, _ = c.shape
        r = zeros((M, C))
        m1 = 1./( self.fuzzyness_coefficient - 1. )
        for k in range(M):
            den = numpy_sum((x[k] - c)**2., axis=1)
            frac = outer(den, 1./den)**m1
            r[k, :] = 1. / numpy_sum(frac, axis=1)
        self.__membership_degrees = r
        return self.__membership_degrees

    def step(self):
        """ Method called on each iteration and returns
            error for this iteration, using old_membership_degrees
            and newly computed self.__membership_degrees.
        """
        old_membership_degrees = self.__membership_degrees
        self.membership()
        self.compute_centers()
        return sum((self.__membership_degrees[i1][i2] - old_membership_degrees[i1][i2]) ** 2\
                        for i1 in xrange(len(self.__membership_degrees)) for i2 in xrange(len(self.__centers)))

    def __call__(self, max_error=1.e-10, max_iterations=100):
        error = 1.
        self.__iterations = 0
        while error > max_error and self.__iterations < max_iterations:
            error             = self.step()
            self.__iterations = self.__iterations + 1

        return self.centers